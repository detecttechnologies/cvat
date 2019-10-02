import { AnyAction, Dispatch, ActionCreator } from 'redux';
import { ThunkAction } from 'redux-thunk';
import { TasksQuery } from '../reducers/interfaces';

import _cvat from '../../../cvat-core/dist/cvat-core.node';

const cvat: any = _cvat;

export enum TasksActionTypes {
    GET_TASKS_SUCCESS = 'GET_TASKS_SUCCESS',
    GET_TASKS_FAILED = 'GET_TASKS_FAILED',
}

export function getTasksSuccess(array: any[], count: number, query: any): AnyAction {
    const action = {
        type: TasksActionTypes.GET_TASKS_SUCCESS,
        payload: {
            array,
            count,
        },
    };

    if (query !== null) {
        (action.payload as any).query = query;
    }

    return action;
}

export function getTasksFailed(error: any, query: any): AnyAction {
    const action = {
        type: TasksActionTypes.GET_TASKS_FAILED,
        payload: {
            error,
        },
    };

    if (query !== null) {
        (action.payload as any).query = query;
    }

    return action;
}

export function getTasksAsync(query: TasksQuery):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        let result = null;
        try {
            // todo: request according to query
            result = await cvat.tasks.get();
        } catch (error) {
            dispatch(getTasksFailed(error, query));
            return;
        }

        const array = Array.from(result);
        dispatch(getTasksSuccess(array, result.count, query));
    };
}
