/*
* Adapted from https://github.com/PrivTap/PrivTap
*/

import router from "@/router";
import type { ErrorResponse } from "../model/error_model";
import type { AxiosError } from "axios";
import { useToast } from "vue-toastification";
import RoutingPath from "@/router/routing_path";

export default function axiosCatch(error: any): void {
    const err = error as AxiosError;
    var message = "An error occured";
    if (err.response?.data) {
        message = (err.response?.data as ErrorResponse<Object>).detail;
    }
    if (err.response?.status == 401) {
        router.replace(RoutingPath.AUTH)
    }
    useToast().error(message);
}