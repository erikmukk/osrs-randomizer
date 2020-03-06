const initialState = () => {
    return {
        monster: null,
        isLoading: false,
        isPoisonous: false,
        isDragonfire: false
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
        setItem (state, item) {
          state.isDragonfire = item ? item.isDragonfire : false;
          state.isPoisonous = item ? item.isPoisonous : false;
          state.monster = item;
        }
    },

    actions: {
        getOneMonster ({commit}, queryParams) {
            commit('setLoading', true);
            commit('setItem', null);
            fetch(`${process.env.VUE_APP_API_URL}/one_monster?${makeQueryString(queryParams)}`)
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                commit('setItem', resp)
            })
            .catch(err => {
            })
            .finally(() => {
                commit('setLoading', false)
            })
        }
    },

    getters: {
        oneMonster: state => state.monster,
        isLoading: state => state.isLoading,
				isPoisonous: state => state.isPoisonous,
				isDragonfire: state => state.isDragonfire
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
