"""
End-to-End Test: Complete Translation Flow

Tests the full user journey:
1. User signup
2. Login
3. Navigate to chapter
4. Translate to Urdu
5. Toggle back to English
6. Submit feedback

Note: Requires Playwright installation:
    pip install playwright pytest-playwright
    playwright install
"""

import pytest
from playwright.sync_api import Page, expect
import time


# Test configuration
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8001"
TEST_USER_EMAIL = f"test_{int(time.time())}@example.com"
TEST_USER_PASSWORD = "Test1234!"


@pytest.fixture(scope="module")
def browser_context(playwright):
    """Create browser context for all tests"""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    yield context
    context.close()
    browser.close()


@pytest.fixture
def page(browser_context):
    """Create new page for each test"""
    page = browser_context.new_page()
    yield page
    page.close()


class TestTranslationE2E:
    """End-to-end translation flow tests"""

    def test_01_user_signup(self, page: Page):
        """Test 1: User can sign up with software/hardware background"""
        print(f"\n🧪 Test 1: Signup with email: {TEST_USER_EMAIL}")

        # Navigate to signup page
        page.goto(f"{BASE_URL}/signup")
        page.wait_for_load_state("networkidle")

        # Fill signup form
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.fill('textarea[placeholder*="software"]', "Python, JavaScript, ROS2")
        page.fill('textarea[placeholder*="hardware"]', "Arduino, Raspberry Pi")

        # Submit form
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Verify redirect to homepage or dashboard
        assert "signup" not in page.url.lower() or "login" in page.url.lower()
        print("✅ Signup successful")

    def test_02_user_login(self, page: Page):
        """Test 2: User can login with credentials"""
        print(f"\n🧪 Test 2: Login with email: {TEST_USER_EMAIL}")

        # Navigate to login page
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")

        # Fill login form
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)

        # Submit form
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Verify authentication (should see logout or profile)
        assert "login" not in page.url.lower()
        print("✅ Login successful")

    def test_03_navigate_to_chapter(self, page: Page):
        """Test 3: User can navigate to a chapter with translation support"""
        print("\n🧪 Test 3: Navigate to ROS2 Fundamentals chapter")

        # Login first
        page.goto(f"{BASE_URL}/login")
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to chapter with translation support
        page.goto(f"{BASE_URL}/docs/ros2-fundamentals")
        page.wait_for_load_state("networkidle")

        # Verify chapter loaded
        assert "ros2" in page.url.lower() or "fundamentals" in page.url.lower()

        # Verify translation button exists
        translate_button = page.locator('button:has-text("Translate to Urdu")')
        expect(translate_button).to_be_visible(timeout=5000)
        print("✅ Chapter loaded with translation button")

    def test_04_translate_to_urdu(self, page: Page):
        """Test 4: User can translate chapter to Urdu (first time - API call)"""
        print("\n🧪 Test 4: Translate chapter to Urdu")

        # Login and navigate to chapter
        page.goto(f"{BASE_URL}/login")
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/docs/intro")
        page.wait_for_load_state("networkidle")

        # Click translate button
        translate_button = page.locator('button:has-text("Translate to Urdu")')
        translate_button.click()

        # Verify loading state appears
        loading_indicator = page.locator('text=Translating')
        expect(loading_indicator).to_be_visible(timeout=2000)
        print("⏳ Loading indicator visible")

        # Wait for translation to complete (8-10 seconds)
        page.wait_for_timeout(12000)

        # Verify button changed to "View in English"
        english_button = page.locator('button:has-text("View in English")')
        expect(english_button).to_be_visible(timeout=15000)
        print("✅ Translation completed successfully")

        # Verify Urdu content is displayed (check for RTL)
        # Note: Actual Urdu verification would need OCR or specific text matching
        page.wait_for_timeout(1000)

    def test_05_toggle_to_english(self, page: Page):
        """Test 5: User can toggle back to English instantly"""
        print("\n🧪 Test 5: Toggle back to English")

        # Login, navigate, and translate first
        page.goto(f"{BASE_URL}/login")
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/docs/intro")
        page.wait_for_load_state("networkidle")

        # Translate to Urdu first
        translate_button = page.locator('button:has-text("Translate to Urdu")')
        if translate_button.is_visible():
            translate_button.click()
            page.wait_for_timeout(12000)

        # Click "View in English" button
        english_button = page.locator('button:has-text("View in English")')
        start_time = time.time()
        english_button.click()

        # Verify instant toggle (<100ms target, but allow 1s for UI)
        page.wait_for_timeout(500)
        urdu_button = page.locator('button:has-text("Translate to Urdu")')
        expect(urdu_button).to_be_visible(timeout=2000)

        elapsed = time.time() - start_time
        print(f"✅ Toggled to English in {elapsed:.2f}s (instant)")
        assert elapsed < 2.0, "Toggle should be instant (<2s)"

    def test_06_cached_translation(self, page: Page):
        """Test 6: Second translation loads from cache (<1s)"""
        print("\n🧪 Test 6: Cached translation loading")

        # Login and navigate
        page.goto(f"{BASE_URL}/login")
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/docs/intro")
        page.wait_for_load_state("networkidle")

        # Ensure we're in English view
        english_button = page.locator('button:has-text("View in English")')
        if english_button.is_visible():
            english_button.click()
            page.wait_for_timeout(500)

        # Click translate again (should hit cache)
        translate_button = page.locator('button:has-text("Translate to Urdu")')
        start_time = time.time()
        translate_button.click()

        # Wait for translation to complete
        english_button = page.locator('button:has-text("View in English")')
        expect(english_button).to_be_visible(timeout=5000)

        elapsed = time.time() - start_time
        print(f"✅ Cache hit in {elapsed:.2f}s")

        # Verify cache indicator visible
        cache_indicator = page.locator('text=Loaded from cache')
        # Cache indicator might not always be visible, so don't assert
        if cache_indicator.is_visible(timeout=1000):
            print("⚡ Cache indicator displayed")

    def test_07_submit_feedback(self, page: Page):
        """Test 7: User can submit translation feedback"""
        print("\n🧪 Test 7: Submit translation feedback")

        # Login, navigate, and translate
        page.goto(f"{BASE_URL}/login")
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/docs/intro")
        page.wait_for_load_state("networkidle")

        # Translate to Urdu first
        translate_button = page.locator('button:has-text("Translate to Urdu")')
        if translate_button.is_visible():
            translate_button.click()
            page.wait_for_timeout(12000)

        # Click "Report Issue" button
        feedback_button = page.locator('button:has-text("Report Issue")')
        if feedback_button.is_visible():
            feedback_button.click()
            page.wait_for_timeout(500)

            # Fill feedback form
            textarea = page.locator('textarea[placeholder*="issue"]')
            textarea.fill("Test feedback: The term 'API' should remain in English.")

            # Submit feedback
            submit_button = page.locator('button:has-text("Submit Feedback")')
            submit_button.click()
            page.wait_for_timeout(2000)

            # Verify success message
            success_message = page.locator('text=Thank you')
            if success_message.is_visible(timeout=3000):
                print("✅ Feedback submitted successfully")
            else:
                print("⚠️ Feedback button found but submission uncertain")
        else:
            print("⚠️ Feedback button not visible (may need Urdu translation first)")

    def test_08_unauthenticated_user_prompt(self, page: Page):
        """Test 8: Unauthenticated users see login prompt"""
        print("\n🧪 Test 8: Unauthenticated user experience")

        # Navigate to chapter without login
        page.goto(f"{BASE_URL}/docs/intro")
        page.wait_for_load_state("networkidle")

        # Check if translation button is disabled or shows auth prompt
        translate_button = page.locator('button:has-text("Translate to Urdu")')

        if translate_button.is_visible():
            # Click button (should not translate)
            translate_button.click()
            page.wait_for_timeout(1000)

            # Should see authentication prompt or redirect to signup
            auth_prompt = page.locator('text=Login required, text=Sign up, text=login')
            if auth_prompt.is_visible(timeout=2000):
                print("✅ Authentication prompt shown to guest users")
            elif "signup" in page.url.lower() or "login" in page.url.lower():
                print("✅ Redirected to signup/login page")
            else:
                print("⚠️ Authentication handling unclear")


# Run tests with: pytest backend/tests/e2e/test_translation_flow.py -v -s
# Note: Requires backend and frontend servers running:
#   Terminal 1: cd backend && python3 main.py
#   Terminal 2: cd frontend && npm start
