// import React from 'react'
// import signupImg from "../assets/signup.png";
// import Template from './Template';


// function Signup({ setIsLoggedIn }) {
//   return (
//     <div>
//        <Template
//         title="Welcome Back" desc1 = "Fly High with us to Ensure Your Building's Strength" desc2 = "revolutionise your creation using drones" image ={signupImg} formType="signup" setIsLoggedIn={setIsLoggedIn}
//       />
//     </div>
//   );
// }

// export default Signup


import React from 'react'
import signupImg from "../assets/signup.png"
import Template from '../Components/Template'

const Signup = ({setIsLoggedIn}) => {
  return (
    <Template
          title="Welcome Back"
          desc1 = "Fly High with us to Ensure Your Building's Strength" 
          desc2 = "revolutionise your creation using drones"
          image={signupImg}
          formtype="signup" 
          setIsLoggedIn={setIsLoggedIn}
      />
  )
}

export default Signup