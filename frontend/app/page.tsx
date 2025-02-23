// app/page.tsx
import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/nextjs';
import LandingPage from './components/Home/LandingPage';


export const metadata = {
  title: 'SentiMetrics',
  icons: {
    icon: '/vercel.svg',
  },
};

export default function HomePage() {
  return (
    <div>
      <SignedIn>
        <LandingPage />
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </div>
  );
}
