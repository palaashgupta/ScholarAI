<template>
  <div class="about-us-page container my-5">
    <h1 class="text-center mb-4">About ScholarAI</h1>

    <div class="row align-items-center mb-5">
      <div class="col-md-6">
        <img
          :src="aboutImg"
          alt="About ScholarAI"
          class="img-fluid rounded shadow"
        />
      </div>
      <div class="col-md-6">
        <h3>Who We Are</h3>
        <p>
          ScholarAI is an advanced research paper search platform designed to help students, researchers, and professionals quickly find, read, and analyze scientific literature.
        </p>
        <p>
          Currently, we leverage the <strong>Semantic Scholar API</strong> to provide access to millions of academic papers and abstracts, giving you accurate and relevant results.
        </p>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-md-12">
        <h3>Our Mission</h3>
        <p>
          Our mission is to make academic research accessible and efficient for everyone. By offering intelligent search capabilities, paper summaries, and analytics, we aim to save your time while providing high-quality insights.
        </p>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-md-12">
        <h3>Future Plans</h3>
        <p>
          In the near future, we plan to expand our search database to include multiple APIs to cover a wider range of scientific content. Some examples include:
        </p>
        <ul>
          <li><strong>PubMed API</strong> - Access to life sciences and biomedical research papers.</li>
          <li><strong>arXiv API</strong> - Preprints in physics, mathematics, computer science, and more.</li>
          <li><strong>CrossRef API</strong> - Metadata for scholarly publications worldwide.</li>
        </ul>
        <p>
          This expansion will allow ScholarAI to provide more comprehensive results and analytics for all research domains.
        </p>
      </div>
    </div>

    <div class="row text-center">
      <div class="col-md-12">
        <router-link to="/" class="btn btn-primary btn-lg">Back to Home</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import aboutImg from '../assets/about_us.png';
</script>

<style scoped>
.about-us-page h1 {
  font-weight: bold;
}

.about-us-page p,
.about-us-page ul {
  font-size: 1.1rem;
  line-height: 1.6;
}

.about-us-page ul {
  margin-top: 1rem;
}

.about-us-page img {
  max-height: 400px;
  object-fit: cover;
}
</style>
