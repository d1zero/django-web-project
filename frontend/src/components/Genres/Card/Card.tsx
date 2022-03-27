import React from 'react';
import {
    Card,
    CardActions,
    CardContent,
    CardMedia,
    Button,
    Typography,
} from '@mui/material';
import { IGenre } from '../../../types/Genre/IGenre';
import { Link } from 'react-router-dom';

interface CardProps {
    item: IGenre
}

const GenreCard: React.FC<CardProps> = ({ item }) => {
    return (
        <Card>
            <Link to='/' style={{ textDecoration: 'none' }}>
                <CardMedia
                    component="img"
                    height="200"
                    image={`${import.meta.env.VITE_MEDIA_URL}${item.cover}`}
                    alt={item.name}
                    style={{objectFit: 'cover'}}
                />
                <CardContent style={{ minHeight: 200 }} >
                    <Typography gutterBottom variant="h5" component="div" align="center">
                        {item.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {item.description}
                    </Typography>
                </CardContent>
            </Link>
        </Card>
    );
}

export default GenreCard