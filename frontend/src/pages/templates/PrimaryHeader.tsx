import { Anchor, Burger, Container, Drawer, Group, Header, Title, createStyles, rem } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useState } from "react";

const HEADER_HEIGHT = rem(60);

const useStyle = createStyles((theme) => ({
    inner: {
        height: HEADER_HEIGHT,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
    },

    links: {
        height: HEADER_HEIGHT,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'end',


        [theme.fn.smallerThan('sm')]: {
            display: 'none',
        },
    },

    burger: {
        [theme.fn.largerThan('sm')]: {
            display: 'none',
        },
    },

    link: {
        fontSize: rem(16),
        color: theme.colorScheme === 'dark' ? theme.colors.dark[1] : theme.colors.gray[6],
        padding: `${rem(7)} ${theme.spacing.lg}`,

        borderBottom: `${rem(2)} solid transparent`,
        transition: 'border-color 100ms ease, color 100ms ease',

        '&:hover': {
            color: theme.colorScheme === 'dark' ? theme.white : theme.black,
            textDecoration: 'none',
        },
    },

    activeLink: {
        color: theme.colorScheme === 'dark' ? theme.white : theme.black,
        borderBottomColor: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 5 : 6],
    }

}));

interface LinkProps {
    links: {
        link: string;
        label: string;
    }[]
}



const PrimaryHeader = ({ links }: LinkProps) => {
    const [opened, { toggle }] = useDisclosure(false);
    const { classes, cx } = useStyle();
    const [active, setActive] = useState(0);

    const items = links.map((item, index) => (
        <Anchor
            href={item.link}
            key={item.link}
            className={cx(classes.link, { [classes.activeLink]: index === active })}
            onClick={(event) => {
                event.preventDefault();
                setActive(index);
            }}
        >
            {item.label}
        </Anchor>
    ));


    return <Header height={HEADER_HEIGHT} zIndex={100}>
        <Drawer opened={opened} onClose={toggle} title="KOTH">
            Links to be added
        </Drawer>
        <Container className={classes.inner}>
            <Title order={3} weight={800}>KOTH</Title>
            <Group spacing={0} position="right" className={classes.links}>
                {items}
            </Group>
            <Burger opened={opened} onClick={toggle} className={classes.burger} size="sm"></Burger>
        </Container>
    </Header >;
};

export default PrimaryHeader;