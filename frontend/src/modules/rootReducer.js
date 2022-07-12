import axios from "axios";
import {ActionTypes} from "../const";


const initialState = {
    token: '',
    text: '',
    postUid: ''
};

export const rootReducer = (state = initialState, action) => {
    switch (action.type) {
        case ActionTypes.SEND_COMMENT:

            if (state.text) {
                axios.post('/blog/add_comment', state).then(response => {
                    let data = response.data
                    let div = document.createElement('div')
                    div.className = 'comment'
                    div.innerHTML = `<h1>Прокомментировал: <span>${data.username}</span></h1>
                                    <p>Говорит, что: <span>${data.text}</span></p>`
                    document.querySelector('#commentLine').append(div)
                })
            } else {
                alert('Сообщение не должно быть пустым')
            }
            document.querySelector('#comment').value = ''

            return {
                ...state,
                text: ''
            }
        case ActionTypes.UPDATE_TEXT:
            return {
                ...state,
                text: action.payload
            }
        case ActionTypes.GET_POST:
            return {
                ...state,
                postUid: action.payload
            }
        case ActionTypes.GET_USER:
            return {
                ...state,
                token: action.payload
            }
        default:
            return state
    }
}
