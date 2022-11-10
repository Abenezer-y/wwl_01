import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore/lite';
// import {collection, query, orderBy, onSnapshot} from "firebase/firestore"


const firebaseConfig = {
apiKey: "AIzaSyAtFQlTQinKOUjgkT98sigDenbOqjLmM-c",
authDomain: "arete-prma.firebaseapp.com",
projectId: "arete-prma",
storageBucket: "arete-prma.appspot.com",
messagingSenderId: "118823315758",
appId: "1:118823315758:web:c4d3139f965ab624a9f2bf"};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);



export default db;