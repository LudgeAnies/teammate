import { createRouter, createWebHistory } from "vue-router";

// auth
import Register from "../views/auth/Register.vue";
import Login from "../views/auth/Login.vue";
import EmailVerificationSent from "../views/auth/EmailVerificationSent.vue";
import ConfirmEmail from "../views/auth/ConfirmEmail.vue";
import SocialAuthComplete from "@/views/auth/SocialAuthComplete.vue";
import Profile from "../views/Profile.vue";

// reset pass
import ResetPassword from "../views/auth/ResetPassword.vue";
import ResetPasswordConfirm from "../views/auth/ResetPasswordConfirm.vue";

// organization
import Organizations from "../views/organizations/Organizations.vue";
import InviteToOrg from "../views/organizations/InviteToOrg.vue";

const routes = [
    // auth
    { path: '/register', name: 'register', component: Register },
    { path: '/login', name: 'login', component: Login },
    { path: '/email_verification', name: 'email_verification_sent', component: EmailVerificationSent },
    { path: '/confirm-email/:uid/:token/', name: 'confirm-email', component: ConfirmEmail },
    { path: '/social-auth-complete', name: 'social-auth-complete', component: SocialAuthComplete },
    { path: '/profile', name: 'profile', component: Profile },

    //reset pass
    { path: '/reset_password', name: 'reset_password', component: ResetPassword },
    { path: '/reset_password_confirm', name: 'reset_password_confirm', component: ResetPasswordConfirm },

    { path: '/organizations', name: 'organizations', component: Organizations },
    { path: '/invite_organization', name: 'invite_to_org', component: InviteToOrg },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router