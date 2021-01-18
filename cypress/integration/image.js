describe("Image features", () => {
    before(() => {
        cy.clearCookies();
        cy.login();
    });

    beforeEach(() => {
        Cypress.Cookies.preserveOnce("sessionid", "csrftoken", "astrobin_lang", "cookielaw_accepted");
        cy.visitImage();
    });

    it("should like and unlike an image", () => {
        cy.likeImage();
    });

    it("should comment on an image", () => {
        cy.comment();
    });
});
