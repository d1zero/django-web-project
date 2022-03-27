import { makeAutoObservable } from 'mobx'

export default class Store {
    loading: boolean = true

    constructor() {
        makeAutoObservable(this)
    }

    setLoading(bool: boolean) {
        this.loading = bool
    }
}