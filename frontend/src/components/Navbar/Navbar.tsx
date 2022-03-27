import React from 'react';
import { AppBar, Box, Button, Container, IconButton, Menu, MenuItem, Toolbar, Tooltip, Typography, useMediaQuery } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { Link } from 'react-router-dom'
import { NavbarLinksStyles, UserLinksStyles } from './NavbarStyles'
import MenuIcon from '@mui/icons-material/Menu';
import { INavbarPage } from './NavbarTypes';

const pages: INavbarPage[] = [
    { name: 'Каталог', link: '/catalog' },
    { name: 'Треки', link: '/tracks' },
    { name: 'Плейлисты', link: '/playlists' },
    { name: 'Подкасты', link: '/podcasts' },
];
const settings: INavbarPage[] = [
    { name: 'Профиль', link: '/profile' },
    { name: 'Выйти', link: '/logout' },
];

const Navbar = () => {
    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
    const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);

    const isMobile = !useMediaQuery('(min-width: 900px)')

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    return (
        <AppBar position="static">
            <Container maxWidth="lg">
                <Toolbar disableGutters>
                    {isMobile ?
                        <>
                            <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
                                <IconButton
                                    size="large"
                                    aria-label="account of current user"
                                    aria-controls="menu-appbar"
                                    aria-haspopup="true"
                                    onClick={handleOpenNavMenu}
                                    color="inherit"
                                >
                                    <MenuIcon />
                                </IconButton>
                                <Menu
                                    id="menu-appbar"
                                    anchorEl={anchorElNav}
                                    anchorOrigin={{
                                        vertical: 'bottom',
                                        horizontal: 'left',
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'left',
                                    }}
                                    open={Boolean(anchorElNav)}
                                    onClose={handleCloseNavMenu}
                                    sx={{
                                        display: { xs: 'block', md: 'none' },
                                    }}
                                >
                                    {pages.map((page) => (
                                        <MenuItem key={page.link} onClick={handleCloseNavMenu}>
                                            <Typography textAlign="center">{page.name}</Typography>
                                        </MenuItem>
                                    ))}
                                </Menu>
                            </Box>

                            <Typography
                                variant="h6"
                                noWrap
                                component="div"
                                sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
                            >
                                MUSICALITY
                            </Typography>
                        </>
                        :
                        <>
                            <Typography
                                variant="h4"
                                noWrap
                                component="div"
                                sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
                            >
                                <Link to='/' style={NavbarLinksStyles}>
                                    MUSICALITY
                                </Link>
                            </Typography>
                            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                                {pages.map((page) => (
                                    <Link key={page.link} to={page.link} style={NavbarLinksStyles}>
                                        <Button
                                            onClick={handleCloseNavMenu}
                                            sx={{ my: 2, color: 'white', display: 'block' }}
                                        >
                                            {page.name}
                                        </Button>
                                    </Link>
                                ))}
                            </Box>
                        </>
                    }

                    <Box sx={{ flexGrow: 0 }}>
                        <Tooltip title="Open settings">
                            <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                                <AccountCircleIcon fontSize='large' style={{ color: '#fff' }} />
                            </IconButton>
                        </Tooltip>
                        <Menu
                            sx={{ mt: '45px' }}
                            id="menu-appbar"
                            anchorEl={anchorElUser}
                            anchorOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            open={Boolean(anchorElUser)}
                            onClose={handleCloseUserMenu}
                        >
                            {settings.map((setting) => (
                                <MenuItem key={setting.link} onClick={handleCloseUserMenu}>
                                    <Link to={setting.link} style={UserLinksStyles}>
                                        <Typography textAlign="center">{setting.name}</Typography>
                                    </Link>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar >
    );
};

export default Navbar;
