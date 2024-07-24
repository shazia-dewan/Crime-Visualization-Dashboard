import React, { useEffect, useState } from 'react';

const BarChart = () => {
  const [image, setImage] = useState(null);

  useEffect(() => {
    fetch('/api/plot/bar')
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setImage(url);
      });
  }, []);

  return (
    <div>
      <h2>Bar Chart</h2>
      {image && <img src={image} alt="Bar Chart" />}
    </div>
  );
};

export default BarChart;
