export const StoneImage = ({ color, name, image }) => {
    return (
        <span>
            <img src={image} alt={`${color}-${name}`} />
        </span>
    );
};
