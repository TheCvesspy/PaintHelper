---
trigger: always_on
---

Never create new users or access tokens unless specifically asked to. Always use the login credentials provided in login_credentials.json for testing purposes.
Always ask if you are to test only the new feature, or do full round of regression testing including the new feature.
If there is no such document, create document TestPlan which will be filled by testing scenarios and their order. When adding new feature add its testing steps also to this TestPlan. Keep the test plan up to date with new development.