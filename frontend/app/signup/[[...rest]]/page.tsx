import { SignUp } from "@clerk/nextjs";

export default function SignupPage() {
  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">Stage 1</p>
        <h1>Sign up</h1>
        <p className="lede">Create a new account so study progress stays tied to the right user.</p>
        <SignUp routing="path" path="/signup" signInUrl="/login" />
      </section>
    </main>
  );
}
