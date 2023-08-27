import PrimaryHeader from "./templates/PrimaryHeader";

const Home = () => {
    return (
        <>
            <PrimaryHeader links={[
                { label: "Home", link: "#" },
                { label: "Games", link: "#2" },
                { label: "Profile", link: "#3" },
            ]} />
        </>
    );
}

export default Home;