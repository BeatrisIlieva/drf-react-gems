export const UserActionCard = ({ category, imageUrl }) => {
    return (
        <>
            <h5>{category}S</h5>
            <img src={imageUrl} alt={`${category}-image`} />
        </>
    );
};
