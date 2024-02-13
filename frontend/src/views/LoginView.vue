<script setup lang="ts">
import TextField from '../components/TextField.vue'
import logoURL from '../assets/logo.png'
import AuthController from '../controllers/auth_controller'
import { ref, computed } from "vue";
import router from "@/router/index";
import RoutingPath from "@/router/routing_path";

var username: string = "";
var password: string = "";

const showLogin = ref<boolean>(true);
const isLoading = ref<boolean>(false);

const isValidPassword = computed(() => {
	if (password.length < 9) {
		return false;
	} else {
		return true;
	}
});

const isValidUsername = computed(() => {
	if (username.length == 0) {
		return false;
	} else {
		return true;
	}
});

const isButtonEnabled = computed(() => {
	if (isLoading.value) return false;
	if (showLogin.value) {
		return username.length > 0 && isValidPassword.value;
	}
	return (
		isValidUsername.value && isValidPassword.value
	);
});

function changeView() {
	showLogin.value = !showLogin.value;
}

async function onSubmitted(event: Event) {
	isLoading.value = true;
	if (event) {
		event.preventDefault();
	}

	if (showLogin.value) {
		const res = await AuthController.login(username, password);
		if (res) router.replace(RoutingPath.HOME);
	} else {
		await _signUp();
	}
	isLoading.value = false;
}

async function _signUp() {
	await AuthController
		.register(username, password)
		.then((res) => {
			if (res === true) {
				changeView();
			}
		});
}
</script>

<template>
	<div id="form-container" class="d-flex align-items-center py-4 bg-body-tertiary">
		<main class="form-signin w-100 m-auto">
			<form>
				<img class="mb-4" style="max-width: 72px;" :src="logoURL" alt="">
				<h1 class="h3 mb-3 fw-normal">{{ showLogin ? "Sign In" : "Create an account" }}</h1>

				<TextField type="text" id="floatingInput" placeholder="Username" label="Username"
					@inputChanged="(new_val) => username = new_val" />
				<TextField type="password" id="floatingPwd" placeholder="Password" label="Password"
					@inputChanged="(new_val) => password = new_val" />

				<button class="btn btn-primary w-100 py-2" type="submit" @click="onSubmitted($event)">{{ showLogin ? "Sign in" : "Sign up" }}</button>
			</form>
			<div class="text-sm text-center justify-center pt-4">
		        <p class="text-secondary">
		            {{
		            	showLogin
		            	? "Don't have an account? "
		            	: "Do you already have an account? "
		            }}
					<button class="fw-medium text-primary hover:text-primary-emphasis" @click="changeView">
			            {{ showLogin ? "Sign Up" : "Login" }}
			        </button>
		        </p>
		    </div>
		</main>
	</div>
</template>

<style scoped>
#form-container {
	height: 100%;
}

.form-signin {
	max-width: 330px;
	padding: 1rem;
}

.form-signin .form-floating:focus-within {
	z-index: 2;
}

.form-signin input[type="email"] {
	margin-bottom: -1px;
	border-bottom-right-radius: 0;
	border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
	margin-bottom: 10px;
	border-top-left-radius: 0;
	border-top-right-radius: 0;
}
</style>