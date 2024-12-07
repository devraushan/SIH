import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ImagePagination from "./ImagePagination";
import { Link } from "react-router-dom";
import Segmented from "./Segmented";

function ImageUploadForm() {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [previewImage1, setPreviewImage1] = useState(null);
  const [previewImage2, setPreviewImage2] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const resultImageRef = useRef(null);

  const handleImage1Change = (e) => {
    const file = e.target.files[0];
    setImage1(e.target.files[0]);
    setPreviewImage1(URL.createObjectURL(file));
  };

  const [images, setImages] = useState([]);

  const handleFolderUpload = (event) => {
    const files = event.target.files;
    const imageUrls = [];
    for (let i = 0; i < files.length; i++) {
      if (files[i].type.startsWith("image/")) {
        imageUrls.push(URL.createObjectURL(files[i]));
      }
    }
    setImages(imageUrls);
  };
  // Sample image data for testing pagination
  const sampleImages = Array.from(
    { length: 100 },
    (_, i) => `https://via.placeholder.com/150?text=Image+${i + 1}`
  );

  // const handleImage2Change = (e) => {
  //   const file = e.target.files[0];
  //   setImage2(e.target.files[0]);
  //   setPreviewImage2(URL.createObjectURL(file));
  // };

  const handleImage2Change = (e) => {
    const files = e.target.files; // This will capture all files in the folder
    const images = [];
    const previews = [];

    // Iterate through all files and process only images
    for (let i = 0; i < files.length; i++) {
      if (files[i].type.startsWith("image/")) {
        images.push(files[i]);
        previews.push(URL.createObjectURL(files[i]));
      }
    }

    if (images.length > 0) {
      setImage2(images); // Save all selected images
      setPreviewImage2(previews); // Save previews of all images
    } else {
      console.warn("No images found in the selected folder.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("image1", image1);
    formData.append("image2", image2);

    try {
      const response = await axios.post(
        "http://localhost:5000/process-images",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob", // We expect the response to be a binary file (image)
        }
      );

      // Create a URL for the result image so we can display it
      const resultImageUrl = URL.createObjectURL(response.data);
      setResultImage(resultImageUrl);
    } catch (error) {
      console.error("Error uploading images:", error);
    }
  };

  useEffect(() => {
    if (resultImage && resultImageRef.current) {
      console.log("Scrolling to the image...");
      resultImageRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [resultImage]);

  return (
    <div className="w-full h-[200vh] text-white bg-gray-800 p-8">
      <h1 className="text-center font-extrabold text-[35px] mb-6">
        Upload Your Images
      </h1>

      <Segmented />

      <div className="p-4 flex justify-center">
        {/* Upload Folder */}
        <label className="inline-flex items-center justify-center bg-red-600 text-white px-6 py-3 rounded-md cursor-pointer">
          Upload Folder
          <input
            type="file"
            webkitdirectory="true"
            directory="true"
            accept="image/*"
            onChange={handleFolderUpload}
            className="hidden"
          />
        </label>
      </div>

      {/* Render ImagePagination if images are uploaded */}
      {images.length > 0 && <ImagePagination images={images} />}

      <div className="flex justify-center">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            {/* <label className="inline-flex items-center justify-center min-h-[80px] min-w-[330px] box-border px-12 py-6 font-medium text-2xl bg-[#e5322d] leading-[28px] align-middle text-white no-underline mb-3 transition-colors duration-300 ease-linear border-0 rounded-3xl shadow-md max-w-[60vw] hover:bg-red-700">
              Choose Image 1
              <input
                type="file"
                accept="image/*"
                onChange={handleImage1Change}
                className="hidden"
                required
              />
            </label> */}

            {previewImage1 && (
              <div className="mt-4">
                <h3 className="text-center text-lg font-semibold">
                  Preview Image 1:
                </h3>
                <img
                  height={150}
                  width={150}
                  src={previewImage1}
                  alt="Preview 1"
                  className="mx-auto border-2 border-gray-400 rounded-lg shadow-md"
                />
              </div>
            )}
          </div>

          <div>
            {/* <label className="inline-flex items-center justify-center min-h-[80px] min-w-[330px] box-border px-12 py-6 font-medium text-2xl bg-[#e5322d] leading-[28px] align-middle text-white no-underline mb-3 transition-colors duration-300 ease-linear border-0 rounded-3xl shadow-md max-w-[60vw] hover:bg-red-700">
              Choose Image 2
              <input
                type="file"
                accept="image/*"
                onChange={handleImage2Change}
                className="hidden"
                required
              />
            </label> */}

            {/* <label className="inline-flex items-center justify-center min-h-[80px] min-w-[330px] box-border px-12 py-6 font-medium text-2xl bg-[#e5322d] leading-[28px] align-middle text-white no-underline mb-3 transition-colors duration-300 ease-linear border-0 rounded-3xl shadow-md max-w-[60vw] hover:bg-red-700">
  Choose Folder
  <input
    type="file"
    webkitdirectory="true"
    directory="true"
    accept="image/*"
    onChange={handleImage2Change}
    className="hidden"
    required
  />
</label> */}

            {/* {previewImage2 && (
              <div className='mt-4'>
                <h3 className='text-center text-lg font-semibold'>Preview Image 2:</h3>
                <img
                  height={150}
                  width={150}
                  src={previewImage2}
                  alt="Preview 2"
                  className='mx-auto border-2 border-gray-400 rounded-lg shadow-md'
                />
              </div>
            )} */}

            {previewImage2 && (
              <div className="mt-4">
                <h3 className="text-center text-lg font-semibold">
                  Preview Images:
                </h3>
                <div className="grid grid-cols-6 gap-4">
                  {previewImage2.map((preview, index) => (
                    <img
                      key={index}
                      height={100}
                      width={150}
                      src={preview}
                      alt={`Preview ${index + 1}`}
                      className="mx-auto border-2 border-gray-400 rounded-lg shadow-md object-cover"
                    />
                  ))}
                </div>
              </div>
            )}
          </div>

          <button
            className="
            bg-blue-500 
            text-white 
            font-semibold 
            py-2 px-4 
            rounded-lg 
            hover:bg-blue-600 
            focus:outline-none 
            focus:ring-2 
            focus:ring-blue-300 
            shadow-md 
            transition-all 
            duration-200 
            ease-in-out
          "
          >
            Submit
          </button>
        </form>
      </div>

      {resultImage && (
        <div ref={resultImageRef} className="mt-8 text-center">
          <h2 className="text-xl font-semibold mb-4">Processed Image:</h2>
          <img
            height={600}
            width={600}
            src={resultImage}
            alt="Result"
            className="mx-auto my-4 border-4 border-gray-300 shadow-lg rounded-lg"
            onLoad={() => {
              console.log("Image loaded, scrolling...");
              resultImageRef.current.scrollIntoView({ behavior: "smooth" });
            }}
          />
        </div>
      )}
    </div>
  );
}

export default ImageUploadForm;
