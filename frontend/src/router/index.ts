import AuthController from "@/controllers/auth_controller";
import { createRouter, createWebHistory } from "vue-router";
import RoutingPath from "./routing_path";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: RoutingPath.BASE,
      name: "base",
      redirect: "/login",
    },
    {
      path: RoutingPath.HOME,
      name: "decks",
      component: () => import("../views/DecksView.vue"),
      meta: {
        requireAuth: true,
      },
    },
    {
      path: RoutingPath.DECK_DETAIL,
      name: "deck/detail",
      component: () => import("../views/DeckDetailView.vue"),
      meta: {
        requireAuth: true,
      },
    },
    {
      path: RoutingPath.DECK_STUDY,
      name: "deck/study",
      component: () => import("../views/StudyView.vue"),
      meta: {
        requireAuth: true,
      },
    },
    {
      path: RoutingPath.DECK_BROWSE,
      name: "deck/cards",
      component: () => import("../views/DeckBrowseView.vue"),
      meta: {
        requireAuth: true,
      },
    },
    {
      path: RoutingPath.CARD_DETAIL,
      name: "card",
      component: () => import("../views/CardDetailView.vue"),
      meta: {
        requireAuth: true,
      },
    },
    {
      path: RoutingPath.AUTH,
      name: "auth",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      redirect: "/home",
    }
  ],
});

/// Router guard to check if user is authenticated
router.beforeEach((to, from, next) => {
  let isAuthenticated = AuthController.isAuthenticated.value;
  if (to.meta.requireAuth && !isAuthenticated) return next(RoutingPath.AUTH);
  if (to.name === "login" && isAuthenticated) return next(RoutingPath.HOME);
  return next();
});

export default router;
