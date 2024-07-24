import React, { useEffect, useState } from 'react';

const PieChart = () => {
  const [image, setImage] = useState(null);

  useEffect(() => {
    fetch('/api/plot/pie')
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setImage(url);
      });
  }, []);

  return (
    <div>
      <h2>Pie Chart</h2>
      {image && <img src={image} alt="Pie Chart" />}
    </div>
  );
};

export default PieChart;
