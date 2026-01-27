import { RegisterForm } from "@/components/auth/RegisterForm";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Register - Todo App",
  description: "Create your account",
};

export default function RegisterPage() {
  return <RegisterForm />;
}
