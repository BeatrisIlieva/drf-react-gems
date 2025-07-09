import { useState, useRef } from "react";
import { Icon } from "../../../../reusable/icon/Icon";
import styles from "./ProfilePhotoUpload.module.scss";

export const ProfilePhotoUpload = ({
    currentPhoto,
    onPhotoUpdate,
    isUploading = false,
}) => {
    const [preview, setPreview] = useState(null);
    const [dragOver, setDragOver] = useState(false);
    const fileInputRef = useRef(null);

    const handleFileSelect = (file) => {
        if (!file.type.startsWith("image/")) {
            alert("Please select an image file");
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert("Image size should be less than 5MB");
            return;
        }

        setPreview(URL.createObjectURL(file));
        onPhotoUpdate(file);
    };

    const handleInputChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelect(e.target.files[0]);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = () => {
        setDragOver(false);
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const displayPhoto = preview || currentPhoto;
    const hasPhoto = Boolean(displayPhoto);

    return (
        <div className={styles["photo-upload-container"]}>
            <div
                className={`${styles["photo-wrapper"]} ${
                    dragOver ? styles["drag-over"] : ""
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={handleClick}
            >
                {currentPhoto ? (
                    <img
                        src={displayPhoto}
                        alt="Profile"
                        className={styles["profile-photo"]}
                    />
                ) : (
                    <img
                        src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1750959197/user-1699635_1280_z3dgxn.png"
                        alt="Profile"
                        className={styles["profile-photo"]}
                    />
                )}

                <div
                    className={`${styles["overlay"]} ${
                        isUploading ? styles["uploading"] : ""
                    }`}
                >
                    {isUploading ? (
                        <div className={styles["loading-spinner"]} />
                    ) : (
                        <>
                            <Icon name="camera" fontSize={24} />
                            <span className={styles["upload-text"]}>
                                {hasPhoto ? "Change Photo" : "Add Photo"}
                            </span>
                        </>
                    )}
                </div>
            </div>

            <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleInputChange}
                className={styles["hidden-input"]}
            />

            <p className={styles["helper-text"]}>
                Click to upload or drag and drop
                <br />
                <span className={styles["file-info"]}>
                    JPG, PNG or GIF (max 5MB)
                </span>
            </p>
        </div>
    );
};
