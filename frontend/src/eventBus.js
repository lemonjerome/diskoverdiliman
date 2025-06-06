import { reactive } from "vue";

export const eventBus = reactive({
  events: {},
  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  },
  emit(event, ...args) {
    if (this.events[event]) {
      this.events[event].forEach((callback) => callback(...args));
    }
  },
  off(event, callback) {
    if (this.events[event]) {
      this.events[event] = this.events[event].filter((cb) => cb !== callback);
    }
  },
});