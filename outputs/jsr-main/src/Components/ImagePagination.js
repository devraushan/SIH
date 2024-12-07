import React, { useState } from "react";

const ImagePagination = ({ images }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const imagesPerPage = 25;

  const indexOfLastImage = currentPage * imagesPerPage;
  const indexOfFirstImage = indexOfLastImage - imagesPerPage;

  const currentImages = images.slice(indexOfFirstImage, indexOfLastImage);
  const totalPages = Math.ceil(images.length / imagesPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="mt-4">
      <h3 className="text-center text-lg font-semibold">Preview Images:</h3>

      <div className="grid grid-cols-5 gap-4">
        {currentImages.map((image, index) => (
          <img
            key={index}
            src={image}
            alt={`Preview ${index + 1}`}
            className="mx-auto border-2 border-gray-400 rounded-lg shadow-md object-cover"
            style={{
              height: "150px",
              width: "150px",
            }}
          />
        ))}
      </div>

      <div className="flex justify-center items-center mt-6 space-x-4">
        {Array.from({ length: totalPages }, (_, index) => (
          <button
            key={index}
            onClick={() => handlePageChange(index + 1)}
            className={`px-4 py-2 rounded-md ${
              currentPage === index + 1
                ? "bg-blue-600 text-white"
                : "bg-gray-300 text-black hover:bg-gray-400"
            }`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ImagePagination;
