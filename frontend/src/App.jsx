import React, { useState } from 'react';
import axios from 'axios';
import './css_files/imageProcessor.css';

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

    return (
        <div className="container">
            <h1>Image to Coloring Book</h1>
            <div className="contros">
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload and Process</button>
            </div>
            {processedImage && (
                <div>
                    <h2>Processed Image:</h2>
                    <img src={processedImage} alt="Processed" />
                </div>
            )}
        </div>
    );
}

export default ImageProcessor;
