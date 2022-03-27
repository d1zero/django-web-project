import React, { useState, useEffect, useContext } from 'react'
import { Grid } from '@mui/material'
import GenreCard from '../../components/Genres/Card/Card'
import $api from '../../http'
import { Context } from '../../main'
import { IGenre } from '../../types/Genre/IGenre'

const GenresListPage = () => {
    const { store } = useContext(Context)
    const [genres, setGenres] = useState<IGenre[] | null>([])

    useEffect(() => {
        store.setLoading(true)
        $api.get('/genres/').then(({ data }) => {
            setGenres(data)
            setTimeout(() => {
                store.setLoading(false)
            }, 1000);
        })
    }, [])

    if (!store.loading && genres) {
        return (
            <Grid container spacing={6}>
                {genres.map(genre => {
                    return (
                        <Grid item key={genre.id} md={4} >
                            <GenreCard item={genre} />
                        </Grid>
                    )
                })}
            </Grid>
        )
    } else { return null }
}

export default GenresListPage