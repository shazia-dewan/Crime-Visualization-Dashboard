import React, { useEffect, useState } from 'react';

const LineChart = () => {
  const [image, setImage] = useState(null);

  useEffect(() => {
    fetch('/api/plot/line')
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setImage(url);
      });
  }, []);

  return (
    <div>
      <h2>Line Chart</h2>
      {image && <img src={image} alt="Line Chart" />}
    </div>
  );
};

export default LineChart;
