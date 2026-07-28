import { SignIn } from "@clerk/nextjs";

export default function LoginPage() {
  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">Stage 1</p>
        <h1>Log in</h1>
        <p className="lede">Use your Learning Assistant account to access saved documents and future study activity.</p>
        <SignIn routing="path" path="/login" signUpUrl="/signup" />
      </section>
    </main>
  );
}
