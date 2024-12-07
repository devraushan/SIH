// import React from 'react'
// import Signup from './Signup'
// import SignupForm from './SignupForm'
// import LoginForm from './LoginForm'
// import frame from '../assets/frame.png'

// const Template = ({title,desc1 ,desc2,image,formType,setIsLoggedIn}) => {
//   return (
//     <div className='flex w-11/12 max-w-[1160px] py-12 mx-auto gap-y-12'>
//       <div >
//         <h1>{title}</h1>
//         <p>
//             <span>{desc1}</span>
//             <span>{desc2}</span>
//         </p>

//         {formType === "signup" ? (<SignupForm setIsLoggedIn ={setIsLoggedIn}/>) : (<LoginForm setIsLoggedIn ={setIsLoggedIn}/>)}

//         <div>
//             <div></div>
//             <p>Or</p>
//             <div></div>
//         </div>

//         <button>
//             <p>
//                 signup with google
//             </p>
//         </button>
//       </div>
    
//     <div>
//         <img src={frame} alt="frame" width={558} height={504} loading='lazy'/>
//         <img src={image} alt="frame" width={490} height={504} loading='lazy'/>
//     </div>
//     </div>
//   )
// }

// export default Template


import React from "react";
import frameImage from "../assets/frame.png";
import SignupForm from "./SignupForm";
import LoginForm from "./LoginForm";
import { FcGoogle } from 'react-icons/fc';

const Template = ({ title, desc1, desc2, image, formtype, setIsLoggedIn }) => {
  console.log("Ye raha mera form type");
  console.log(formtype);

  return (
    <div className="flex justify-between flex-row w-11/12 max-w-[1160px] py-12 mx-auto gap-x-12 gap-y-0">
      {/* Content Section */}
      <div className="w-11/12 max-w-[450px]">
        <h1 className="text-richblack-5 font-semibold text-[1.875rem] leading-[2.375rem]">
          {title}
        </h1>
        <p className="text=[1.25rem] leading-[1.625rem] mt-4">
          <span className="text-richblack-100">{desc1}</span>
          <br />
          <span className="text-blue-100">{desc2}</span>
        </p>

        {/* Form */}
        {formtype === "signup" ? (
          <SignupForm setIsLoggedIn={setIsLoggedIn} />
        ) : (
          <LoginForm setIsLoggedIn={setIsLoggedIn} />
        )}

        {/* OR Section */}
        <div className="flex w-full items-center my-4 gap-x-2">
          <div className="w-full h-[1px] bg-richblack-700"></div>
          <p className="text-richblack-700 font-medium leading[1.375rem]">OR</p>
          <div className="w-full h-[1px] bg-richblack-700"></div>
        </div>
        <button className="w-full flex justify-center items-center rounded-[8px] font-medium text-richblack-100 border border-richblack-700 px-[12px] py-[8px] gap-x-2 mt-6">
          <FcGoogle/>
          <p>Sign Up with Google</p>
        </button>
      </div>

      {/* Image Section */}
      <div className="relative w-11/12 max-w-[450px]">
        <img
          src={frameImage}
          alt="Pattern"
          width={558}
          height={504}
          loading="lazy"
        />
        <img
          src={image}
          alt="Students"
          width={558}
          height={490}
          loading="lazy"
          className="absolute -top-4 right-4"
        />
      </div>
    </div>
  );
};

export default Template;