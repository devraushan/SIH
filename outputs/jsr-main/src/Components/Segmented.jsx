import React, { useState } from 'react';
import Papa from 'papaparse';

function Segmented() {
  const [data, setData] = useState([]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      Papa.parse(file, {
        header: true,
        complete: (results) => {
          setData(results.data);
        },
      });
    }
  };

  return (
    <div className="Segmented">
      <input type="file" accept=".csv" onChange={handleFileUpload} />

      {data.length ? (
        <table className="table">
          <thead>
            <tr>
              <th>House</th>
              <th>Coordinates</th>
              <th>MeasuredHeight (ft)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row.House}</td>
                <td>{row.Coordinates}</td>
                <td>{row.MeasuredHeight}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </div>
  );
}

export default Segmented;
