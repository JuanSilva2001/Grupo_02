import PropTypes from "prop-types";
import React, { useState } from "react";
import "./style/BoxUpload.css";

export const BoxUpload = ({ texto = "Carregue seu arquivo aqui" }) => {
    const [fileName, setFileName] = useState("");
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setFileName(file.name);
        }
    };

    return (
        <div className="box-upload">
            <div className="texto">{fileName || texto}</div>
            <input
                type="file"
                className="upload-input"
                onChange={handleFileChange}
                id='Arquivo'
            />
            <svg
                className="upload-icon"
                width="42"
                height="42"
                viewBox="0 0 42 42"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <g id="Group">
                    <path
                        id="Vector"
                        d="M31 15.004C35.35 15.028 37.706 15.222 39.242 16.758C41 18.516 41 21.344 41 27V29C41 34.658 41 37.486 39.242 39.244C37.486 41 34.656 41 29 41H13C7.344 41 4.514 41 2.758 39.244C1 37.484 1 34.658 1 29V27C1 21.344 1 18.516 2.758 16.758C4.294 15.222 6.65 15.028 11 15.004"
                        stroke="#09BC8A"
                        stroke-width="1.5"
                        stroke-linecap="round"
                    />
                    <path
                        id="Vector_2"
                        d="M21 27V1M21 1L27 8M21 1L15 8"
                        stroke="#09BC8A"
                        stroke-width="1.5"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    />
                </g>
            </svg>
        </div>
    );
};

BoxUpload.propTypes = {
    texto: PropTypes.string,
};