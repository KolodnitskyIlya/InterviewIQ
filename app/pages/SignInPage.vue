<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, auto, auto, auto, auto, auto, *, auto" class="container">
      <Label row="0" text="Welcome back" class="title" />
      <Label
        row="1"
        text="Sign in to continue your interview prep"
        class="subtitle"
        textWrap="true"
      />

      <StackLayout row="2" class="form">
        <Label text="Email" class="fieldLabel" />
        <TextField
          v-model="email"
          hint="your.email@example.com"
          class="input"
          keyboardType="email"
          autocorrect="false"
          autocapitalizationType="none"
        />

        <Label text="Password" class="fieldLabel fieldSpacing" />
        <TextField
          v-model="password"
          hint="******"
          class="input"
          secure="true"
        />

        <Label
          text="Forgot password?"
          class="forgotLink"
          horizontalAlignment="right"
        />
      </StackLayout>

      <Button row="3" text="Sign In" class="primaryButton" @tap="signIn" />

      <GridLayout row="4" columns="*, auto, *" class="divider">
        <StackLayout col="0" class="dividerLine" />
        <Label col="1" text="or continue with" class="dividerText" />
        <StackLayout col="2" class="dividerLine" />
      </GridLayout>

      <StackLayout row="5">
        <Button text="  Sign in with Apple" class="appleButton" />
        <Button text="✉  Sign in with Google" class="googleButton" />
      </StackLayout>

      <FlexboxLayout
        row="7"
        class="footer"
        justifyContent="center"
        alignItems="center"
      >
        <Label text="Don't have an account?" class="footerText" />
        <Label text=" Sign up" class="footerLink" @tap="goToSignUp" />
      </FlexboxLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { defineComponent } from "nativescript-vue";
import HomePage from "./HomePage.vue";
import SignUpPage from "./SignUpPage.vue";

export default defineComponent({
  name: "SignInPage",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    signIn() {
      this.$navigateTo(HomePage, {
        clearHistory: true,
      });
    },
    goToSignUp() {
      this.$navigateTo(SignUpPage);
    },
  },
});
</script>

<style scoped>
.page {
  background-color: #f3f4f6;
}

.container {
  width: 100%;
  height: 100%;
  padding-top: 58;
  padding-right: 30;
  padding-bottom: 24;
  padding-left: 30;
}

.title {
  font-size: 46;
  font-weight: 700;
  color: #0f172a;
  font-family: "Poppins";
}

.subtitle {
  margin-top: 8;
  font-size: 16;
  font-weight: 600;
  color: #6b7280;
  font-family: "Poppins";
}

.form {
  margin-top: 28;
}

.fieldLabel {
  font-size: 18;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8;
  font-family: "Poppins";
}

.fieldSpacing {
  margin-top: 10;
}

.input {
  height: 58;
  border-width: 1;
  border-color: #9ca3af;
  border-radius: 20;
  padding-right: 20;
  padding-left: 20;
  font-size: 20;
  color: #111827;
  background-color: #f3f4f6;
  placeholder-color: #9ca3af;
  font-family: "Poppins";
}

.forgotLink {
  margin-top: 10;
  color: #4f46e5;
  font-size: 16;
  font-weight: 500;
  font-family: "Poppins";
}

.primaryButton {
  margin-top: 18;
  height: 62;
  border-radius: 22;
  color: #ffffff;
  font-size: 18;
  font-weight: 600;
  font-family: "Poppins";
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

.divider {
  margin-top: 20;
  margin-bottom: 14;
  vertical-align: middle;
}

.dividerLine {
  height: 1;
  background-color: #c7cdd7;
  margin-top: 11;
}

.dividerText {
  color: #9ca3af;
  font-size: 15;
  font-weight: 600;
  margin-right: 12;
  margin-left: 12;
  font-family: "Poppins";
}

.appleButton {
  height: 56;
  border-radius: 20;
  background-color: #050505;
  color: #ffffff;
  font-size: 18;
  font-weight: 500;
  font-family: "Poppins";
}

.googleButton {
  height: 56;
  border-radius: 20;
  border-width: 1;
  border-color: #9ca3af;
  background-color: #f3f4f6;
  color: #111827;
  font-size: 18;
  font-weight: 500;
  margin-top: 10;
  font-family: "Poppins";
}

.footer {
  padding-bottom: 8;
}

.footerText {
  font-size: 16;
  color: #111827;
  font-family: "Poppins";
}

.footerLink {
  font-size: 16;
  color: #4f46e5;
  font-weight: 500;
  font-family: "Poppins";
}
</style>
