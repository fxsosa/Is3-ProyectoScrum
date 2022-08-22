<template>
  <div>
      <div v-show="!profile" id="g-signin2"></div>
      <div v-if="profile">
        <pre>{{ profile }}</pre>
        <button @click="signOut">Sign Out</button>
      </div>
    </div>
</template>

<script>
export default {
  mounted() {
    this.initGoogleAuth();
    this.renderGoogleAuthButton();
  },

  data() {
    return {
      profile: null
    };
  },

  methods: {
    onSignIn(user) {
      const profile = user.getBasicProfile();
      const fullName = profile.getName();
      const email = profile.getEmail();
      const imageUrl = profile.getImageUrl();
      this.profile = { fullName, email, imageUrl };
    },

    signOut() {
      var auth2 = window.gapi.auth2.getAuthInstance();
      auth2.signOut().then(() => {
        console.log("User signed out");
        this.profile = null;
      });
    },

    initGoogleAuth() {
      window.gapi.load("auth2", function () {
        window.gapi.auth2.init();
      });
    },

    renderGoogleAuthButton() {
      window.gapi.signin2.render("g-signin2", {
        onsuccess: this.onSignIn
      });
    }
  }
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
