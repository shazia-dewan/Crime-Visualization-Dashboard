import React, { useEffect, useState } from 'react';

const Heatmap = () => {
  const [image, setImage] = useState(null);

  useEffect(() => {
    fetch('/api/plot/heatmap')
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setImage(url);
      });
  }, []);

  return (
    <div>
      <h2>Heatmap</h2>
      {image && <img src={image} alt="Heatmap" />}
    </div>
  );
};

export default Heatmap;
