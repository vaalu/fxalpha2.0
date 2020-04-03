import { REFRESH_STOCKS } from '../ReduxConstants'

export const DashboardActions = {
	statCardRefreshEquities : (payload:boolean) => {
		return {
			type:REFRESH_STOCKS,
			payload: payload
		}
	}, 
	statCardRefreshEquitiesCount : (payload:number) => {
		return {
			type:REFRESH_STOCKS,
			payload: payload
		}
	}
}