import React from 'react';
import { Link } from 'react-router-dom';
function ladingPage() {
  const scrollToSection = (sectionId) => {
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="font-sans">
      {/* Header */}


      {/* Hero Section */}
      <section className="bg-cover bg-center h-screen text-white flex flex-col items-center justify-center" style={{ backgroundImage: 'url(/drones-bg.jpg)' }}>
        <h2 className="text-5xl font-bold mb-4">Empowering the Future with Drones</h2>
        <p className="text-xl mb-6">create greateness using innovative drone technology</p>


        <Link to="/model"> 
          <button  className="bg-orange-500 hover:bg-orange-600 text-white py-3 px-8 rounded-full">Check out</button>
        </Link>

      </section>

      {/* About Section */}
      <section id="about" className="py-16 px-6 text-center bg-gray-100">
        <h2 className="text-4xl font-semibold mb-6">About Us</h2>
        <p className="text-lg">At Aerial Insight, we leverage advanced drone technology to assess the structural integrity and strength of buildings. Our innovative approach allows for detailed inspections of hard-to-reach areas, providing real-time data on potential weaknesses, cracks, or structural vulnerabilities.</p>
      </section>

      {/* Services Section */}
      <section id="services" className="py-16 px-6 text-center">
        <h2 className="text-4xl font-semibold mb-10">Services</h2>
        <div className="grid gap-10 sm:grid-cols-1 md:grid-cols-3">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-semibold mb-4">Drone-Based Structural Inspections</h3>
            <p>Our drones perform detailed aerial inspections to identify structural weaknesses, cracks, and other potential issues in buildings. This service allows for fast, accurate, and non-invasive assessments of building strength, including difficult-to-reach areas like rooftops and facades..</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-semibold mb-4">Real-Time Data Analysis</h3>
            <p>We provide real-time data processing and analysis from drone inspections, offering immediate insights into the structural integrity of a building. Our AI-driven analytics help detect issues such as material degradation, corrosion, or shifts in load-bearing components.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-semibold mb-4">Periodic Monitoring and Reporting</h3>
            <p>We offer ongoing monitoring services to track the structural health of buildings over time. Our periodic drone inspections and reports help ensure that your building remains strong and safe, reducing the risk of future failures or costly repairs.</p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-16 px-6 text-center bg-gray-100">
        <h2 className="text-4xl font-semibold mb-6">Contact Us</h2>
        <p>Interested in partnering or learning more? Reach out to us via email: <a href="mailto:info@dronestartups.com" className="text-orange-500">info@droneMaster.com</a></p>
      </section>


    </div>
  );
}

export default ladingPage;
