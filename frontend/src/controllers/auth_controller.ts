/*
* Adapted from https://github.com/PrivTap/PrivTap
*/

import type { BaseResponse } from "../model/response_model";
import type { UserModel } from "../model/user_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";

let reference = ref<UserModel | null>(null);

interface IAuthController {
    login(username: string, password: string): Promise<UserModel | null>;
    logout(): Promise<boolean>;
    register(username: string, password: string): Promise<boolean>;
    setUser(newUser: UserModel | null): void;
}

export class AuthController extends BaseController<UserModel | null> implements IAuthController {

    isAuthenticated = computed(() => reference.value != null);

    async login(username: string, password: string): Promise<UserModel | null> {
        const body = {
            username: username,
            password: password,
        };
        const res = await super.post<UserModel>(
            "/login",
            { body: body, message: "Login Successful!" }
        );
        this.setUser(res);
        return res;
    }

    async logout(): Promise<boolean> {
        const res = await super.get("/logout", { message: "Logout Successful!" });
        this.setUser(null);
        if (res == null) return false;
        return true;
    }

    async register(username: string, password: string): Promise<boolean> {
        const body = {
            username: username,
            password: password,
        };
        const res = await super.post("/signup", { body: body, message: "Registration Successful!" });
        return res != null;
    }

    setUser(newUser: UserModel | null): void {
        reference.value = newUser;
        if (newUser) {
            localStorage.setItem("user", JSON.stringify(newUser));
        } else {
            localStorage.removeItem("user");
        }
    }
    /**
     * Return the object reference of this controller. The controller is a singleton, so the reference is the same for all the class
     */
    getRef(): Ref<UserModel | null> {
        return reference;
    }


}

export default new AuthController();