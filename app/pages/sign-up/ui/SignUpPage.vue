<template>
  <Page actionBarHidden="true" class="page">
    <GridLayout rows="auto, auto, auto, auto, auto, *, auto" class="container">
      <Label row="0" text="Create Account" class="title" />
      <Label
        row="1"
        text="Start your interview preparation journey"
        class="subtitle"
        textWrap="true"
      />

      <StackLayout row="2" class="form">
        <Label text="Full Name" class="fieldLabel" />
        <TextField
          v-model="fullName"
          hint="Danil Kolbasenko"
          class="input"
          autocorrect="false"
        />

        <Label text="Email" class="fieldLabel fieldSpacing" />
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

        <Label text="Confirm Password" class="fieldLabel fieldSpacing" />
        <TextField
          v-model="confirmPassword"
          hint="******"
          class="input"
          secure="true"
        />
      </StackLayout>

      <Button
        row="3"
        :text="isSubmitting ? 'Creating Account...' : 'Create Account'"
        class="primaryButton"
        :isEnabled="!isSubmitting"
        @tap="signUp"
      />

      <Label row="4" class="termsText" textWrap="true">
        <FormattedString>
          <Span text="By creating an account, you agree to our " />
          <Span text="Terms of Service" color="#4f46e5" />
          <Span text=" and " />
          <Span text="Privacy Policy" color="#4f46e5" />
        </FormattedString>
      </Label>

      <FlexboxLayout
        row="6"
        class="footer"
        justifyContent="center"
        alignItems="center"
      >
        <Label text="Already have an account?" class="footerText" />
        <Label text=" Sign in" class="footerLink" @tap="goToSignIn" />
      </FlexboxLayout>
    </GridLayout>
  </Page>
</template>

<script lang="ts">
import { alert } from "@nativescript/core";
import { defineComponent } from "nativescript-vue";
import { ApiError, interviewIqApi, saveAuthSession } from "@/shared";
import PersonalizeExperiencePage from "@/pages/personalize-experience";

function errorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message;
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return "Something went wrong. Please try again.";
}

export default defineComponent({
  name: "SignUpPage",
  data() {
    return {
      fullName: "",
      email: "",
      password: "",
      confirmPassword: "",
      isSubmitting: false,
    };
  },
  methods: {
    async signUp() {
      if (this.isSubmitting) {
        return;
      }

      const fullName = this.fullName.trim();
      const email = this.email.trim().toLowerCase();
      const password = this.password.trim();
      const confirmPassword = this.confirmPassword.trim();

      if (fullName.length < 2 || !email || !password) {
        await alert({
          title: "Validation error",
          message: "Please fill in full name, email, and password.",
          okButtonText: "OK",
        });
        return;
      }

      if (password !== confirmPassword) {
        await alert({
          title: "Validation error",
          message: "Password and confirmation do not match.",
          okButtonText: "OK",
        });
        return;
      }

      this.isSubmitting = true;

      try {
        const auth = await interviewIqApi.signUp({
          full_name: fullName,
          email,
          password,
        });
        saveAuthSession(auth);

        this.$navigateTo(PersonalizeExperiencePage, {
          clearHistory: true,
        });
      } catch (error) {
        await alert({
          title: "Sign Up failed",
          message: errorMessage(error),
          okButtonText: "OK",
        });
      } finally {
        this.isSubmitting = false;
      }
    },
    goToSignIn() {
      this.$navigateBack();
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
  padding-top: 54;
  padding-right: 30;
  padding-bottom: 24;
  padding-left: 30;
}

.title {
  font-size: 44;
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
  margin-top: 22;
}

.fieldLabel {
  font-size: 17;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6;
  font-family: "Poppins";
}

.fieldSpacing {
  margin-top: 8;
}

.input {
  height: 52;
  border-width: 1;
  border-color: #9ca3af;
  border-radius: 19;
  padding-right: 20;
  padding-left: 20;
  font-size: 18;
  color: #111827;
  background-color: #f3f4f6;
  placeholder-color: #9ca3af;
  font-family: "Poppins";
}

.primaryButton {
  margin-top: 16;
  height: 60;
  border-radius: 22;
  color: #ffffff;
  font-size: 18;
  font-weight: 600;
  font-family: "Poppins";
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

.termsText {
  margin-top: 12;
  margin-right: 0;
  margin-left: 0;
  font-size: 12;
  line-height: 16;
  text-align: center;
  color: #9ca3af;
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
