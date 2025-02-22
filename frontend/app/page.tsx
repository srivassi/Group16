//Pages used to navigate between componenets 


/* 1 */
//Imports 
import { SignedIn } from '@clerk/nextjs';
import Home from './components/Home/Home.jsx'


/* 2 */
//Title of the browser page 
export const metadata = {
  title: 'Home', // title
  icons: {
    icon: '/vercel.svg', // logo'
  },  
};


/* 3 */
//Main display 
export default function HomePage() {
  return (
    <div> 
      <div> 
        <SignedIn>

          <Home/>

        </SignedIn>
      </div>
    </div>
  );
}
