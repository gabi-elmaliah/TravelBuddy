import Hero from "../components/Hero";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import QuestionnaireForm from "../components/QuestionnaireForm";

function Questionnaire() {
  return (
    <>
      <Navbar />
      <Hero
        cName="hero-mid"
        heroImg="https://images.unsplash.com/photo-1569839333583-7375336cde4b?q=80&w=1930&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        title="Questionnaire"
        btnClass="hide"
      />
      <QuestionnaireForm/>
      <Footer />
    </>
  );
}

export default Questionnaire;