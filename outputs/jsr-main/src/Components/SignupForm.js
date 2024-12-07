// import React, { useState } from 'react'
// import {AiOutlineEye,AiOutlineEyeInvisible} from "react-icons/ai"
// import { useNavigate} from "react-router-dom";
// import { toast } from "react-hot-toast";


// const SignupForm = ({setIsLoggedIn}) => {

//     const navigate = useNavigate();

//     const [formData,setFormData] = useState(
//         {firstName:"",lastName:"",email:"",password:"",confirmPassword:""}
//     )

//     function changeHandler(event){
//         setFormData( (prevData) =>(
//           {...prevData,[event.target.name]:event.target.value} 
//         ))
//     }

//     const [showPassword,setShowPassword] = useState('false'); 


//     function submitHandler(event){
//         event.preventDefault();

//         if(formData.password !== formData.confirmPassword){
//             toast.error("Passwords do not matc")
//             return;
//         }
//         setIsLoggedIn(true);
//         navigate("/dashboard")
//         toast.success("Account created");
//         console.log(formData)
        
//       }
//   return (
//     <div>
//       <div>
//         <button>Student</button>
//         <button>Instructor</button>
//       </div>

//       <form onSubmit={submitHandler}>
//         <div>
//             <label >
//                 <p>First Name<sup>*</sup></p>
//                 <input type="text" required name='firstName' value={formData.firstName} placeholder='Enter first name' onChange={changeHandler}/>
//             </label>
//             <label >
//                 <p>Last Name<sup>*</sup></p>
//                 <input type="text" required name='lastName' value={formData.lastName} placeholder='Enter last name' onChange={changeHandler}/>
//             </label>
//         </div>

//         <label >
//             <p>Email id<sup>*</sup></p>
//             <input type="email" required name='email' value={formData.email} placeholder='abc@gmail.com' onChange={changeHandler}/>
//         </label>

//         <div>
//             <label >
//                 <p>Create Password<sup>*</sup></p>
//                 <input type={!showPassword ? ("text") : ("password")} required name='password' value={formData.password} placeholder='Enter Password' onChange={changeHandler}/>
//                 <span onClick={()=>{setShowPassword((prev) => !prev)}}>
//                     {
//                         !showPassword? (<AiOutlineEyeInvisible/>) : (<AiOutlineEye/>)
//                     }
//                 </span>
//             </label>
//             <label >
//                 <p>Confirm Password<sup>*</sup></p>
//                 <input type={!showPassword ? ("text") : ("password")} required name ='confirmPassword' value={formData.confirmPassword} placeholder='Enter Password' onChange={changeHandler}/>
//                 <span onClick={()=>{setShowPassword((prev) => !prev)}}>
//                     {
//                         !showPassword? (<AiOutlineEyeInvisible/>) : (<AiOutlineEye/>)
//                     }
//                 </span>
//             </label>

            
//         </div>

//         <button>Create Account</button>
//       </form>
//     </div>
//   )
// }

// export default SignupForm


import React, { useState } from 'react'
import toast from 'react-hot-toast';
import  {AiOutlineEye, AiOutlineEyeInvisible} from "react-icons/ai";
import { useNavigate } from 'react-router-dom';

const SignupForm = ({setIsLoggedIn}) => {

  const navigate = useNavigate();

  const [formData,setFormData] = useState({
    firstname:"",
    lastname:"",
    email:"",
    password:"",
    confirmPassword:"",
  })


  const [showPassword,setShowPassword]= useState(false);
  const [showConfirmPassword,setShowConfirmPassword]= useState(false);
  const [accountType, setAccountType] = useState("student");


  function changeHandler(event){
    setFormData( (prevData) => (
      {
        ...prevData,
        [event.target.name]:event.target.value
      }
    ))
  }

  function submitHandler(event){
    event.preventDefault();
    if(formData.password != formData.confirmPassword){
      toast.error("Passwords do not match");
      return;
    }

    setIsLoggedIn(true);
    toast.success("Account Created");

    const accountData={
      ...formData
    };
    const finalData = {
      ...accountData,
      accountType
    }


    console.log("Printing final account data");
    console.log(accountData);

    navigate("/dashboard");
  }

  return (
    <div>
      {/* student-nstructor tab */}

      {/* <div className='flex bg-richblack-800 p-1 gap-x-1 my-6 rounded-full max-w-max'>
        <button
        className={`${accountType === "student" 
          ?
          "bg-richblack-900 text-richblack-5":
          "bg-transparent text-richblack-200"
        } py-2 px-5 rounded-full transition-all duration-200 `}
        onClick={()=> setAccountType("student")}>
          student
        </button>
        <button
        className={`${accountType === "instructor" 
          ?
          "bg-richblack-900 text-richblack-5":
          "bg-transparent text-richblack-200"
        } py-2 px-5 rounded-full transition-all duration-200 `}
        onClick={()=> setAccountType("instructor")}>
          Instructor
        </button>
      </div> */}

      <form onSubmit={submitHandler}>
        {/* firstName and lastname */}

        <div className='flex gap-4 mt-[20px]'>
           <label className='w-full relative '>
          <p className='text-[0.875rem] text-richblack-5 mb-1 leading-[1.375rem] '>
            First Name 
            <sup  className='text-pink-200'>*</sup></p>
          <input 
            required
            type="text"
            name='firstname'
            onChange={changeHandler}
            placeholder='Enter First Name'
            value={formData.firstname}
            className='bg-richblack-800 rounded-[0.5rem] text-richblack-5 w-full p-[12px] '

          />
           </label >
           <label  className='w-full relative'>
          <p className='text-[0.875rem] text-richblack-5 mb-1 leading-[1.375rem] '>Last Name <sup className='text-pink-200'>*</sup></p>
          <input 
            required
            type="text"
            name='lastname'
            onChange={changeHandler}
            placeholder='Enter Last Name'
            value={formData.lastname}
            className='bg-richblack-800 rounded-[0.5rem] text-richblack-5 w-full p-[12px] '

          />
           </label>
        </div>
        {/* Email Address */}

        <div className='w-full relative mt-[20px]'>
            
        <label >
          <p className='text-[0.875rem] text-richblack-5 mb-1 leading-[1.375rem] '>Email Address <sup className='text-pink-200'>*</sup></p>
          <input 
            required
            type="email"
            name='email'
            onChange={changeHandler}
            placeholder='Enter Email Address'
            value={formData.email}
            className='bg-richblack-800 rounded-[0.5rem] text-richblack-5 w-full p-[12px] '

          />
           </label>

        </div>
           
        {/* createPassword and Confirm password */}

        <div className='w-full flex gap-x-4 mt-[20px] '>
       
        <label className='w-full relative'>
          <p  className='text-[0.875rem] text-richblack-5 mb-1 leading-[1.375rem] '>Create Password <sup className='text-pink-200'>*</sup></p>
          <input 
            required
            type={showPassword ? ("text") : ("password")}
            name='password'
            onChange={changeHandler}
            placeholder='Enter  Password '
            value={formData.password}
            className='bg-richblack-800 rounded-[0.5rem] text-richblack-5 w-full p-[12px] '

          />
        <span 
         className='absolute right-3 top-[38px] cursor-pointer '
        onClick={()=> setShowPassword((prev) => !prev)}>
          {showPassword ?
           (<AiOutlineEyeInvisible fontSize={24} fill='#AFB2BF'/>):
           (<AiOutlineEye fontSize={24} fill='#AFB2BF'/>) }
        </span>          
        </label>

        <label  className='w-full relative'>
          <p  className='text-[0.875rem] text-richblack-5 mb-1 leading-[1.375rem] '>Confirm Password <sup className='text-pink-200'>*</sup></p>
          <input 
            required
            type={showConfirmPassword ? ("text") : ("password")}
            name='confirmPassword'
            onChange={changeHandler}
            placeholder='Enter Confirm Password '
            value={formData.confirmPassword}
             className='bg-richblack-800 rounded-[0.5rem] text-richblack-5 w-full p-[12px] '

          />
        <span
        className='absolute right-3 top-[38px] cursor-pointer '
        onClick={()=> setShowConfirmPassword((prev) => !prev)}>
          {showConfirmPassword ?
           (<AiOutlineEyeInvisible fontSize={24} fill='#AFB2BF' />):(<AiOutlineEye  fontSize={24} fill='#AFB2BF'/>) }
        </span>          
        </label>
        </div>

        <button className='bg-yellow-50 w-full rounded-[8px] font-medium text-richblack-900 px-[12px] py-[8px] mt-6'>
          Create Account
        </button>
      </form>

    </div>
  )
}

export default SignupForm