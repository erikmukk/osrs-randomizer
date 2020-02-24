const initialState = () => {
    return {
        items: [],
        isLoading: false
    }
}

export default {
    namespaced: true,

    state: {
        ...initialState()
    },

    mutations: {
        setLoading (state, isLoading) {
            state.isLoading = isLoading;
        },
        setItems (state, items) {
            state.items = items;
        }
    },

    actions: {
        getAllInventory ({commit}, queryParams) {
            commit('setLoading', true);
            commit('setItems', []);
            fetch(`${process.env.VUE_APP_API_URL}/full_inventory?${makeQueryString(queryParams)}`)
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                commit('setItems', resp)
            })
            .catch(err => {
            })
            .then(() => {
                commit('setLoading', false)
            })
        }
    },

    getters: {
        allItems: state => state.items,
        isLoading: state => state.isLoading
    }
}

const makeQueryString = (data) => {
    if (data !== '') {
      let qString = '&'
      Object.keys(data).map(key => {
        qString += `${key}=${data[key]}&`
      })
      return qString;
    }
    return ''
  }