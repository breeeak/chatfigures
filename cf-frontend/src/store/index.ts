import { createStore } from "vuex";
import { config } from "vuex-module-decorators";
// Set rawError to true by default on all @Action decorators
config.rawError = true;

import AuthModule from "@/store/modules/AuthModule";

const store = createStore({
    modules: {
        AuthModule,
    },
});

export default store;