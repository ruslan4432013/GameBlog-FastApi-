import {ActionTypes} from "../const";


export const sendComment = () => {
    return {
        type: ActionTypes.SEND_COMMENT
    }
}

export const getUser = (value) => {
    return {
        type: ActionTypes.GET_USER,
        payload: value
    }
}

export const getPostToken = (value) => {
    return {
        type: ActionTypes.GET_POST,
        payload: value
    }
}

export const updateText = (value) => {
    return {
        type: ActionTypes.UPDATE_TEXT,
        payload: value
    }
}
