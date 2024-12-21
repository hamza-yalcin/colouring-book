import React, { useState } from 'react';
import axios from 'axios';
import './css_files/imageProcessor.css';
import './css_files/navigation.css'

function ImageProcessor() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post('http://127.0.0.1:5000/process-image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                responseType: 'blob', // To handle the image file response
            });

            const url = URL.createObjectURL(response.data);
            setProcessedImage(url);
        } catch (error) {
            console.error('Error processing image:', error);
        }
    };

    const handlePrint = () => {
      window.print()
    }

    return (
      <div>
        <nav className="navbar">
          <h1 className="navbar-title">ColorMe</h1>
        </nav>
        <div className="container">
            <div className="controls">
            <input 
              type="file" 
              onChange={handleFileChange}
              id="file-input"
              className="hidden-file-input"
            />
            <label htmlFor="file-input" className="choose-file-button">
              Choose File
            </label>
            <button onClick={handleUpload} className="process-button">Upload and Process</button>
            </div>
            {processedImage && (
                <div>
                    <h2>Processed Image:</h2>
                    <img id="processed-image" src={processedImage} alt="Processed" className="processed-image"/>
                    <button onClick={handlePrint} className="upload-button">Print Image</button>
                </div>
            )}
        </div>
      </div>
    );
}

export default ImageProcessor;
