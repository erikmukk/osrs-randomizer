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
        },
        replaceOneItem (state, newItem) {
            state.items = state.items.map(item => {
                if (item.slot === newItem.slot) {
                    return newItem
                }
                return item
            })
        }
    },

    actions: {
        getFullEquipment ({commit}, queryParams) {
            commit('setLoading', true);
            commit('setItems', []);
            fetch(`${process.env.VUE_APP_API_URL}/full_gear?${makeQueryString(queryParams)}`)
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                commit('setItems', resp)
            })
            .catch(err => {
            })
            .then(() => {
                commit('setLoading', false);
            })
        },
        getOneEquipmentInSlot ({commit}, {slot, queryParams}) {
            commit('setLoading', true);
            fetch(`${process.env.VUE_APP_API_URL}/one_in_slot?slot=${slot}${makeQueryString(queryParams)}`)
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                commit('replaceOneItem', resp)
            })
            .catch(err => {
            })
            .then(() => {
                commit('setLoading', false);
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
