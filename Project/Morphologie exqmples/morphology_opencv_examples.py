
"""
Morphologie Mathématique - Implémentation Python avec OpenCV
Exemples pratiques d'érosion, dilatation, ouverture et fermeture
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

class MorphologyDemo:
    """Classe de démonstration des opérations morphologiques"""
    
    def __init__(self):
        self.results = {}
        
    def create_test_image(self, image_type: str = 'noise') -> np.ndarray:
        """
        Crée une image de test pour démonstration
        
        Args:
            image_type: 'noise', 'holes', 'text', 'shapes'
        
        Returns:
            Image binaire (numpy array)
        """
        img = np.ones((300, 300), dtype=np.uint8) * 255
        
        if image_type == 'noise':
            # Rectangle avec bruit "poivre"
            cv2.rectangle(img, (50, 50), (250, 250), 0, -1)
            # Ajouter du bruit aléatoire
            noise_points = np.random.randint(0, 300, (100, 2))
            for point in noise_points:
                cv2.circle(img, tuple(point), 2, 0, -1)
                
        elif image_type == 'holes':
            # Rectangle avec trous internes
            cv2.rectangle(img, (50, 50), (250, 250), 0, -1)
            # Créer des trous aléatoires
            holes = np.random.randint(70, 230, (20, 2))
            for hole in holes:
                cv2.circle(img, tuple(hole), 3, 255, -1)
                
        elif image_type == 'text':
            # Texte avec artefacts
            cv2.putText(img, 'MORPH', (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 
                       2, 0, 4)
            # Ajouter des petits points
            for _ in range(30):
                x, y = np.random.randint(0, 300, 2)
                cv2.circle(img, (x, y), 1, 0, -1)
                
        elif image_type == 'shapes':
            # Formes géométriques variées
            cv2.rectangle(img, (50, 50), (150, 150), 0, -1)
            cv2.circle(img, (200, 100), 40, 0, -1)
            cv2.ellipse(img, (120, 220), (60, 30), 0, 0, 360, 0, -1)
            
        return img
    
    def create_structuring_element(self, shape: str = 'rect', 
                                   size: int = 5) -> np.ndarray:
        """
        Crée un élément structurant
        
        Args:
            shape: 'rect', 'cross', 'ellipse'
            size: taille (impaire)
        
        Returns:
            Élément structurant (numpy array)
        """
        if shape == 'rect':
            return cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
        elif shape == 'cross':
            return cv2.getStructuringElement(cv2.MORPH_CROSS, (size, size))
        elif shape == 'ellipse':
            return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
        else:
            # SE personnalisé (exemple : ligne horizontale)
            se = np.zeros((size, size), dtype=np.uint8)
            se[size//2, :] = 1
            return se
    
    def erosion(self, image: np.ndarray, kernel: np.ndarray, 
                iterations: int = 1) -> np.ndarray:
        """
        Applique l'érosion
        
        Formule : A ⊖ B = {z | Bz ⊆ A}
        """
        result = cv2.erode(image, kernel, iterations=iterations)
        return result
    
    def dilation(self, image: np.ndarray, kernel: np.ndarray, 
                 iterations: int = 1) -> np.ndarray:
        """
        Applique la dilatation
        
        Formule : A ⊕ B = {z | B̂z ∩ A ≠ ∅}
        """
        result = cv2.dilate(image, kernel, iterations=iterations)
        return result
    
    def opening(self, image: np.ndarray, kernel: np.ndarray, 
                iterations: int = 1) -> np.ndarray:
        """
        Applique l'ouverture (érosion puis dilatation)
        
        Formule : A ○ B = (A ⊖ B) ⊕ B
        Effet : Élimine petits objets, lisse contours externes
        """
        result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, 
                                 iterations=iterations)
        return result
    
    def closing(self, image: np.ndarray, kernel: np.ndarray, 
                iterations: int = 1) -> np.ndarray:
        """
        Applique la fermeture (dilatation puis érosion)
        
        Formule : A • B = (A ⊕ B) ⊖ B
        Effet : Comble petits trous, lisse contours internes
        """
        result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, 
                                 iterations=iterations)
        return result
    
    def gradient(self, image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """
        Calcule le gradient morphologique
        
        Formule : ∇(A) = (A ⊕ B) - (A ⊖ B)
        Effet : Détection de contours
        """
        result = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
        return result
    
    def tophat(self, image: np.ndarray, kernel: np.ndarray, 
               white: bool = True) -> np.ndarray:
        """
        Applique la transformation Top-Hat
        
        White Top-Hat : A - (A ○ B) → Extrait objets clairs
        Black Top-Hat : (A • B) - A → Extrait objets sombres
        """
        if white:
            result = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
        else:
            result = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
        return result
    
    def compare_operations(self, image: np.ndarray, kernel: np.ndarray) -> dict:
        """
        Compare toutes les opérations sur une même image
        
        Returns:
            Dictionnaire avec tous les résultats
        """
        results = {
            'original': image,
            'erosion': self.erosion(image, kernel),
            'dilation': self.dilation(image, kernel),
            'opening': self.opening(image, kernel),
            'closing': self.closing(image, kernel),
            'gradient': self.gradient(image, kernel),
            'tophat': self.tophat(image, kernel)
        }
        return results
    
    def visualize_results(self, results: dict, title: str = "Opérations Morphologiques"):
        """
        Visualise les résultats avec matplotlib
        """
        n_results = len(results)
        cols = 4
        rows = (n_results + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(16, 4*rows))
        axes = axes.flatten() if n_results > 1 else [axes]
        
        for idx, (name, img) in enumerate(results.items()):
            axes[idx].imshow(img, cmap='gray')
            axes[idx].set_title(name.capitalize(), fontsize=12, fontweight='bold')
            axes[idx].axis('off')
            
            # Afficher statistiques
            white_pixels = np.sum(img == 255)
            black_pixels = np.sum(img == 0)
            total_pixels = img.size
            fill_percent = (black_pixels / total_pixels) * 100
            
            stats_text = f"Objets: {black_pixels}\nFond: {white_pixels}\nRemplissage: {fill_percent:.1f}%"
            axes[idx].text(0.02, 0.98, stats_text, 
                          transform=axes[idx].transAxes,
                          fontsize=8, verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Cacher les axes vides
        for idx in range(n_results, len(axes)):
            axes[idx].axis('off')
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def analyze_se_effect(self, image: np.ndarray, operation: str = 'opening'):
        """
        Analyse l'effet de différentes tailles de SE
        """
        sizes = [3, 5, 7, 9, 11]
        results = {'original': image}
        
        for size in sizes:
            kernel = self.create_structuring_element('rect', size)
            if operation == 'opening':
                result = self.opening(image, kernel)
            elif operation == 'closing':
                result = self.closing(image, kernel)
            elif operation == 'erosion':
                result = self.erosion(image, kernel)
            elif operation == 'dilation':
                result = self.dilation(image, kernel)
            
            results[f'{operation}_{size}x{size}'] = result
        
        return results
    
    def demonstrate_use_cases(self):
        """
        Démonstrations de cas d'usage pratiques
        """
        print("=== Démonstration des Cas d'Usage ===\n")
        
        # Cas 1 : Élimination de bruit (salt-and-pepper)
        print("1. Élimination de bruit...")
        img_noise = self.create_test_image('noise')
        kernel = self.create_structuring_element('rect', 3)
        cleaned = self.opening(img_noise, kernel)
        
        results_noise = {
            'Image avec bruit': img_noise,
            'Après Opening 3x3': cleaned
        }
        self.results['noise_removal'] = results_noise
        
        # Cas 2 : Comblement de trous
        print("2. Comblement de trous...")
        img_holes = self.create_test_image('holes')
        filled = self.closing(img_holes, kernel)
        
        results_holes = {
            'Image avec trous': img_holes,
            'Après Closing 3x3': filled
        }
        self.results['hole_filling'] = results_holes
        
        # Cas 3 : Détection de contours
        print("3. Détection de contours...")
        img_shapes = self.create_test_image('shapes')
        kernel_grad = self.create_structuring_element('ellipse', 3)
        contours = self.gradient(img_shapes, kernel_grad)
        
        results_contours = {
            'Formes originales': img_shapes,
            'Contours (Gradient)': contours
        }
        self.results['contour_detection'] = results_contours
        
        # Cas 4 : Extraction de détails
        print("4. Extraction de petits détails...")
        img_text = self.create_test_image('text')
        kernel_th = self.create_structuring_element('rect', 7)
        details = self.tophat(img_text, kernel_th)
        
        results_details = {
            'Texte avec artefacts': img_text,
            'Petits détails (Top-Hat)': details
        }
        self.results['detail_extraction'] = results_details
        
        print("\n✓ Toutes les démonstrations terminées !\n")


# ========================================
# EXEMPLES D'UTILISATION
# ========================================

def exemple_1_comparaison_complete():
    """Exemple 1 : Comparaison de toutes les opérations"""
    print("\n" + "="*60)
    print("EXEMPLE 1 : Comparaison Complète des Opérations")
    print("="*60)
    
    demo = MorphologyDemo()
    
    # Créer image de test
    image = demo.create_test_image('noise')
    kernel = demo.create_structuring_element('rect', 5)
    
    # Comparer toutes les opérations
    results = demo.compare_operations(image, kernel)
    
    # Visualiser
    fig = demo.visualize_results(results, "Comparaison des Opérations Morphologiques")
    plt.savefig('morphology_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Résultats sauvegardés dans 'morphology_comparison.png'")


def exemple_2_effet_taille_se():
    """Exemple 2 : Effet de la taille du SE"""
    print("\n" + "="*60)
    print("EXEMPLE 2 : Effet de la Taille de l'Élément Structurant")
    print("="*60)
    
    demo = MorphologyDemo()
    
    # Créer image avec bruit
    image = demo.create_test_image('noise')
    
    # Tester différentes tailles
    results = demo.analyze_se_effect(image, 'opening')
    
    # Visualiser
    fig = demo.visualize_results(results, "Effet de la Taille du SE sur l'Ouverture")
    plt.savefig('se_size_effect.png', dpi=150, bbox_inches='tight')
    print("✓ Résultats sauvegardés dans 'se_size_effect.png'")


def exemple_3_cas_pratiques():
    """Exemple 3 : Cas d'usage pratiques"""
    print("\n" + "="*60)
    print("EXEMPLE 3 : Cas d'Usage Pratiques")
    print("="*60)
    
    demo = MorphologyDemo()
    demo.demonstrate_use_cases()
    
    # Visualiser chaque cas
    for case_name, results in demo.results.items():
        fig = demo.visualize_results(results, f"Cas d'usage : {case_name}")
        filename = f'usecase_{case_name}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Sauvegardé : {filename}")


def exemple_4_pipeline_complet():
    """Exemple 4 : Pipeline de traitement complet"""
    print("\n" + "="*60)
    print("EXEMPLE 4 : Pipeline de Traitement Complet")
    print("="*60)
    
    demo = MorphologyDemo()
    
    # Image initiale très bruitée
    image = demo.create_test_image('noise')
    kernel = demo.create_structuring_element('rect', 3)
    
    # Pipeline : Opening → Closing → Gradient
    step1 = demo.opening(image, kernel, iterations=1)
    step2 = demo.closing(step1, kernel, iterations=1)
    step3 = demo.gradient(step2, kernel)
    
    results = {
        '1. Original (avec bruit)': image,
        '2. Après Opening': step1,
        '3. Après Closing': step2,
        '4. Contours finaux': step3
    }
    
    fig = demo.visualize_results(results, "Pipeline de Traitement Morphologique")
    plt.savefig('morphology_pipeline.png', dpi=150, bbox_inches='tight')
    print("✓ Pipeline complet sauvegardé dans 'morphology_pipeline.png'")


def exemple_5_elements_structurants():
    """Exemple 5 : Comparaison des différents SE"""
    print("\n" + "="*60)
    print("EXEMPLE 5 : Comparaison des Éléments Structurants")
    print("="*60)
    
    demo = MorphologyDemo()
    image = demo.create_test_image('shapes')
    
    results = {'Original': image}
    
    se_types = [('rect', 'Carré'), ('cross', 'Croix'), ('ellipse', 'Ellipse')]
    
    for se_type, name in se_types:
        kernel = demo.create_structuring_element(se_type, 5)
        result = demo.opening(image, kernel)
        results[f'Opening - {name}'] = result
    
    fig = demo.visualize_results(results, "Comparaison des Éléments Structurants")
    plt.savefig('se_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Comparaison SE sauvegardée dans 'se_comparison.png'")


# ========================================
# FONCTIONS AVANCÉES
# ========================================

def skeleton_by_thinning(image: np.ndarray) -> np.ndarray:
    """
    Squelettisation par amincissement morphologique
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skeleton = np.zeros_like(image)
    
    while True:
        eroded = cv2.erode(image, kernel)
        temp = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(image, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        image = eroded.copy()
        
        if cv2.countNonZero(image) == 0:
            break
    
    return skeleton


def morphological_reconstruction(marker: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Reconstruction morphologique par dilatation géodésique
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    reconstructed = marker.copy()
    
    while True:
        previous = reconstructed.copy()
        dilated = cv2.dilate(reconstructed, kernel)
        reconstructed = cv2.min(dilated, mask)
        
        if np.array_equal(reconstructed, previous):
            break
    
    return reconstructed


# ========================================
# POINT D'ENTRÉE PRINCIPAL
# ========================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" DÉMONSTRATION : MORPHOLOGIE MATHÉMATIQUE avec OpenCV")
    print("="*60)
    
    # Exécuter tous les exemples
    exemple_1_comparaison_complete()
    exemple_2_effet_taille_se()
    exemple_3_cas_pratiques()
    exemple_4_pipeline_complet()
    exemple_5_elements_structurants()
    
    print("\n" + "="*60)
    print(" ✓ TOUTES LES DÉMONSTRATIONS TERMINÉES")
    print("="*60)
    print("\nFichiers générés :")
    print("  - morphology_comparison.png")
    print("  - se_size_effect.png")
    print("  - usecase_*.png (4 fichiers)")
    print("  - morphology_pipeline.png")
    print("  - se_comparison.png")
    print("\nTotal : 8 images de démonstration")
    print("\nUtilisez ces exemples pour votre présentation !")
    print("="*60 + "\n")
