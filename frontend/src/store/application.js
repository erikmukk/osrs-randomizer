const initialState = () => {
    return {
        isNewVersion: false
    }
}

export default {
    namespaced: true,

    state: {
        ...initialState()
    },

    mutations: {
        setIsNewVersion (state) {
            state.isNewVersion = !state.isNewVersion;
        }
        
    },

    actions: {
        changeLayout ({commit}) {
            commit('setIsNewVersion');
        }
    },

    getters: {
        isNewVersion: state => state.isNewVersion,
    }
}
