import React, { useState } from 'react';
import './imageUpload.scss';

function ImageUpload() {
  const [image, setImage] = useState(null);
  const [text, setText] = useState('');

  const handleImageUpload = (e) => {
    // const file = e.target.files[0];
    // const reader = new FileReader();
    // // reader.readAsDataURL(file);
    // console.log(file)

    // const formData = new FormData();
    // formData.append('image', file);

    // reader.onload = () => {
    //   setImage(reader.result);
    //   setText('Image uploaded successfully!');
    // };
    fetch('http://localhost:5000/', {
      method: 'GET',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      // .then(data => {
      //   console.log(data)
      // })
      // .catch(error => {
      //   console.error('There was a problem with the fetch operation:', error);
      // });
  };

  return (
    <div className="container">
      <div className="imageContainer" style={{ textAlign: "center" }}>
        <h2>Upload Image</h2>
        {image && <img src={image} alt="Uploaded" className="image" />}
        <input type="file" onChange={handleImageUpload} accept="image/*" />
      </div>
      <div className="textContainer">
        <h2>Classification</h2>
        <p>{text}</p>
      </div>
    </div>
  );
}

export default ImageUpload;
