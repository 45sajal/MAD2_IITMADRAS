<template>
    <h1>
        AUTHORIZATION ERROR
    </h1>
    <br>
    <div class="Signup">
        <button v-on:click="goback">Go back</button>
    </div>
</template>

<script>
export default{
    methods:{
        goback(){
            this.$router.push({name:'Welcome'})
        }
    }
}
</script>