import logo from './logo.svg';
import './App.css';
import ImageUpload from './components/ImageUpload/imageUpload';
// import ImageUpload from './components/ImageUpload/imageupload';

function App() {
  return (
    <div className="App">
      <h1>Image Classifier</h1>
      <ImageUpload></ImageUpload>
    </div>
  );
}

export default App;
