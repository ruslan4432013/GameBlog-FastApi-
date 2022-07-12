import {bindActionCreators, configureStore} from "@reduxjs/toolkit";
import {rootReducer} from "./modules/rootReducer";
import Cookies from 'js-cookie'
import * as actions from './modules/actions';

const store = configureStore({
    reducer: rootReducer
})

export const update = () => {

    console.log(store.getState())
}
const {updateText, getUser, sendComment, getPostToken} = bindActionCreators(actions, store.dispatch)

store.subscribe(update)


document.querySelector('#comment')?.addEventListener('input', (e) => {
    updateText(e.target.value)
})

document.addEventListener('DOMContentLoaded', () => {
    const token = Cookies.get('token'),
        postUid = Cookies.get('post_uid')
    getPostToken(postUid)

    token && getUser(token)
})

document.querySelector('#submitButton')?.addEventListener('click', (e) => {
    e.preventDefault()
    sendComment()
})
